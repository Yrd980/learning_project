package com.ruoyi.entertainment.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.entertainment.mapper.EntertainmentMapper;
import com.ruoyi.entertainment.domain.Entertainment;
import com.ruoyi.entertainment.service.IEntertainmentService;

/**
 * 娱乐信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-09
 */
@Service
public class EntertainmentServiceImpl implements IEntertainmentService 
{
    @Autowired
    private EntertainmentMapper entertainmentMapper;

    /**
     * 查询娱乐信息
     * 
     * @param id 娱乐信息主键
     * @return 娱乐信息
     */
    @Override
    public Entertainment selectEntertainmentById(Long id)
    {
        return entertainmentMapper.selectEntertainmentById(id);
    }

    /**
     * 查询娱乐信息列表
     * 
     * @param entertainment 娱乐信息
     * @return 娱乐信息
     */
    @Override
    public List<Entertainment> selectEntertainmentList(Entertainment entertainment)
    {
        return entertainmentMapper.selectEntertainmentList(entertainment);
    }

    /**
     * 新增娱乐信息
     * 
     * @param entertainment 娱乐信息
     * @return 结果
     */
    @Override
    public int insertEntertainment(Entertainment entertainment)
    {
        return entertainmentMapper.insertEntertainment(entertainment);
    }

    /**
     * 修改娱乐信息
     * 
     * @param entertainment 娱乐信息
     * @return 结果
     */
    @Override
    public int updateEntertainment(Entertainment entertainment)
    {
        return entertainmentMapper.updateEntertainment(entertainment);
    }

    /**
     * 批量删除娱乐信息
     * 
     * @param ids 需要删除的娱乐信息主键
     * @return 结果
     */
    @Override
    public int deleteEntertainmentByIds(Long[] ids)
    {
        return entertainmentMapper.deleteEntertainmentByIds(ids);
    }

    /**
     * 删除娱乐信息信息
     * 
     * @param id 娱乐信息主键
     * @return 结果
     */
    @Override
    public int deleteEntertainmentById(Long id)
    {
        return entertainmentMapper.deleteEntertainmentById(id);
    }
}
