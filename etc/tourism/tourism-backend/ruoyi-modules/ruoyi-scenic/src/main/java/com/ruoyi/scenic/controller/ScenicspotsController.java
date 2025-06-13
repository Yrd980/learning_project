package com.ruoyi.scenic.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.scenic.domain.Scenicspots;
import com.ruoyi.scenic.service.IScenicspotsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 景点信息Controller
 * 
 * @author ningf
 * @date 2024-07-17
 */
@RestController
@RequestMapping("/scenicspots")
public class ScenicspotsController extends BaseController
{
    @Autowired
    private IScenicspotsService scenicspotsService;

    /**
     * 查询景点信息列表
     */
    @RequiresPermissions("scenic:scenicspots:list")
    @GetMapping("/list")
    public TableDataInfo list(Scenicspots scenicspots)
    {
        startPage();
        List<Scenicspots> list = scenicspotsService.selectScenicspotsList(scenicspots);
        return getDataTable(list);
    }

    /**
     * 导出景点信息列表
     */
    @RequiresPermissions("scenic:scenicspots:export")
    @Log(title = "景点信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Scenicspots scenicspots)
    {
        List<Scenicspots> list = scenicspotsService.selectScenicspotsList(scenicspots);
        ExcelUtil<Scenicspots> util = new ExcelUtil<Scenicspots>(Scenicspots.class);
        util.exportExcel(response, list, "景点信息数据");
    }

    /**
     * 获取景点信息详细信息
     */
    @RequiresPermissions("scenic:scenicspots:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(scenicspotsService.selectScenicspotsById(id));
    }

    /**
     * 新增景点信息
     */
    @RequiresPermissions("scenic:scenicspots:add")
    @Log(title = "景点信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Scenicspots scenicspots)
    {
        return toAjax(scenicspotsService.insertScenicspots(scenicspots));
    }

    /**
     * 修改景点信息
     */
    @RequiresPermissions("scenic:scenicspots:edit")
    @Log(title = "景点信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Scenicspots scenicspots)
    {
        return toAjax(scenicspotsService.updateScenicspots(scenicspots));
    }

    /**
     * 删除景点信息
     */
    @RequiresPermissions("scenic:scenicspots:remove")
    @Log(title = "景点信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(scenicspotsService.deleteScenicspotsByIds(ids));
    }
}
