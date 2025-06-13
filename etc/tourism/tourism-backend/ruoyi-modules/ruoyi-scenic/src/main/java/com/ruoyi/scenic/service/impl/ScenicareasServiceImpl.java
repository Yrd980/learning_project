package com.ruoyi.scenic.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.scenic.mapper.ScenicareasMapper;
import com.ruoyi.scenic.domain.Scenicareas;
import com.ruoyi.scenic.service.IScenicareasService;

/**
 * 景区信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-17
 */
@Service
public class ScenicareasServiceImpl implements IScenicareasService 
{
    @Autowired
    private ScenicareasMapper scenicareasMapper;

    /**
     * 查询景区信息
     * 
     * @param id 景区信息主键
     * @return 景区信息
     */
    @Override
    public Scenicareas selectScenicareasById(Long id)
    {
        return scenicareasMapper.selectScenicareasById(id);
    }

    /**
     * 查询景区信息列表
     * 
     * @param scenicareas 景区信息
     * @return 景区信息
     */
    @Override
    public List<Scenicareas> selectScenicareasList(Scenicareas scenicareas)
    {
        return scenicareasMapper.selectScenicareasList(scenicareas);
    }

    /**
     * 新增景区信息
     * 
     * @param scenicareas 景区信息
     * @return 结果
     */
    @Override
    public int insertScenicareas(Scenicareas scenicareas)
    {
        return scenicareasMapper.insertScenicareas(scenicareas);
    }

    /**
     * 修改景区信息
     * 
     * @param scenicareas 景区信息
     * @return 结果
     */
    @Override
    public int updateScenicareas(Scenicareas scenicareas)
    {
        return scenicareasMapper.updateScenicareas(scenicareas);
    }

    /**
     * 批量删除景区信息
     * 
     * @param ids 需要删除的景区信息主键
     * @return 结果
     */
    @Override
    public int deleteScenicareasByIds(Long[] ids)
    {
        return scenicareasMapper.deleteScenicareasByIds(ids);
    }

    /**
     * 删除景区信息信息
     * 
     * @param id 景区信息主键
     * @return 结果
     */
    @Override
    public int deleteScenicareasById(Long id)
    {
        return scenicareasMapper.deleteScenicareasById(id);
    }
}
